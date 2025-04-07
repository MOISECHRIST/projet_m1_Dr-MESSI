<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Redis;
use Illuminate\Support\Facades\Log;


class UserService{

    protected int $defaultExpiration = 3600;
    protected string $activeUsersKey = 'active_users';

    // Methodes pour communiquer avec le service RabbitMQ
    public function handleUserConnection(string $userId, array $data): User
    {
        // Création ou mise à jour
        $user = User::updateOrCreate(
            ['external_id' => $userId],
            [
                'name' => $data['username'] ?? 'Nouvel Utilisateur',
                'email' => $data['email'] ?? null,
                'role' => $data['role'] ?? 'user',
                'status' => 'connected',
                'last_activity_at' => now()
            ]
        );

        $this->cacheUser($user);
        $this->addToActiveUsers($userId);

        return $user;
    }

    public function handleUserDisconnection(string $userId): void
    {
        if ($user = User::where('external_id', $userId)->first()) {
            $user->update([
                'status' => 'disconnected',
                'last_activity_at' => now()
            ]);
            
            $this->cacheUser($user);
            $this->removeFromActiveUsers($userId);
        }
    }



    public function deleteUser(string $userId): void
    {
        if ($user = User::where('external_id', $userId)->first()) {
            $user->delete();
            $this->removeFromActiveUsers($userId);
            $this->removeUserFromCache($userId);
            Log::info("Utilisateur supprimé", ['user_id' => $userId]);
        }
    }


    
    // Methodes pour obtenir les informations d'un utilisateur
 
    public function getUser($userId){
    
        $cachedUser = Redis::get('user:'. $userId);

        if($cachedUser){
            return json_decode($cachedUser, true);
        }

        $user = User::find($userId);

        if($user){
            $this->cacheUser($user);
            return  $user;
        }

    }

    // Methode pour cacher les utilisateurs dans Redis

    public function cacheUser(User $user): void
    {
        Redis::setex(
            'user:' . $user->id,
            $this->defaultExpiration,
            json_encode($user->toArray(), JSON_THROW_ON_ERROR)
        );
    }

    public function removeUserFromCache($userId){
        Redis::del('user:'.$userId);
    }


    // Méthodes pour gérer les utilisateurs actifs dans Redis

    public function addToActiveUsers(int $userId): void
    {
        Redis::sadd($this->activeUsersKey, $userId);
        Redis::expire($this->activeUsersKey, $this->defaultExpiration);
    }

    public function removeFromActiveUsers(int $userId): void
    {
        Redis::srem($this->activeUsersKey, $userId);
    }

    public function getActiveUsers(): array
    {
        return Redis::smembers($this->activeUsersKey) ?: [];
    }

    public function isUserActive(int $userId): bool
    {
        return (bool) Redis::sismember($this->activeUsersKey, $userId);
    }

}