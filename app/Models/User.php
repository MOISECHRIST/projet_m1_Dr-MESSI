<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class User extends Model
{
    protected $table = 'users';

    protected $fillable = [
        'name',
        'email',
        'role', // client/worker/admin
        'external_id', // ID de l'utilisateur dans le service d'authentification
        'status', // Statut de connexion (connected/disconnected)
        'last_activity_at', // Dernière activité
    ];


    public function comments(){
        return $this->hasMany(Comment::class);
    }

    public function likes(){
        return $this->hasMany(Like::class);
    }


    protected $casts = [
        'last_activity_at' => 'datetime',
    ];

    
    public function markAsConnected()
    {
        $this->update([
            'status' => 'connected',
            'last_activity_at' => now(),
        ]);
    }

    public function markAsDisconnected()
    {
        $this->update([
            'status' => 'disconnected',
            'last_activity_at' => null,
        ]);
    }

    
    public function isInactive($timeoutMinutes = 3600)
    {
        return $this->last_activity_at && $this->last_activity_at->lt(now()->subMinutes($timeoutMinutes));
    }
}