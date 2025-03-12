<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Model;

class Comment extends Model{

    protected $table = 'comments';

    protected $fillable = [
        'content'
    ];

    public function publication(): BelongsTo {
        return $this->belongsTo(Publication::class);
    }


    public function user(): BelongsTo {
        return $this->belongsTo(User::class);
    }
}
