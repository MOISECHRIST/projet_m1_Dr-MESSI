<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Like extends Model{

    protected $table = 'likes';

    protected $fillable = [
        'rate'
    ];

    public function publication(): BelongsTo {
        return $this->belongsTo(Publication::class);
    }


    public function user(): BelongsTo {
        return $this->belongsTo(User::class);
    }
    
}
