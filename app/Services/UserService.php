<?php

namespace App\Services;

use App\Models\User;
use Illuminate\Support\Facades\Redis;
use Illuminate\Support\Facades\Log;


class UserService{

    protected int $defaultExpiration = 3600;

    public function createUser(array $data): User {

        try{
            $user = User::create([
                'name' => $data['name'],
                'email' => $data['email'],
                'role' => $data['role'], 
                'external_id' => $data['user_id'], 
                'status' => 'connected', 
                'last_activity_at' => now()
            ]);

            $this->cacheUser($user);
            
            return $user;

        } catch(\Exception $e){
            Log::error('Erreur lors de la création de l\'utilisateur : ' . $e->getMessage());
            throw $e; 
        }
    }


    public function updateUser(int $userId, array $data): User
    {
        $user = User::findOrFail($userId);
        $user->update($data);

        Redis::set('user:'.$userId, json_encode($user), 'EX', $this->defaultExpiration);

        return $user;
    }


    public function deleteUser(int $userId): void
    {
        $user = User::findOrFail($userId);
        $user->delete();
        $this->removeUseFromCache($userId);
    }

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

    public function cacheUser(User $user){
        Redis::set('user:'. $user->id, json_encode($user), 'EX', $this->defaultExpiration);
    }

    public function removeUseFromCache($userId){
        Redis::del('user:'.$userId);
    }

    public function isUserActive($userId){
        $user = $this->getUser($userId);

        if($user && $user['status'] === 'connected' && !$user->isInactive($this->defaultExpiration)){
            return true;
        }
        return false;
    }
}