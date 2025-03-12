<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Publication extends Model{
    
    protected $table = 'publications';

    protected $fillable = [
        'title',
        'description',
        'type',
        'nbr_view'
    ];

    public function user(): BelongsTo {
        return $this->belongsTo(User::class);
    }

    public function comments(){
        return $this->hasMany(Comment::class);
    }

    public function likes(){
        return $this->hasMany(Like::class);
    }



}
