<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TextImagePublication extends Publication{

    protected $table = 'publications';

    protected $fillable = [
        'image_urls',
        'textContent',
    ];


}
