<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class VideoPublication extends Publication{
    
    protected $table = 'publications';


    protected $fillable = [
        'video_url',
        'nbr_view'
    ];

}
