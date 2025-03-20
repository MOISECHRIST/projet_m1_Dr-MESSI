<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class TextImagePublication extends Publication{

    protected $table = 'publications';

    protected $fillable = [
        'title',
        'description',
        'type',
        'user_id',

        'textContent',
    ];

    protected static function boot(){
        parent::boot();

        static::creating(function ($model) {
            $model->type = 'TextImages';
        });
    }

    // Accessor for text/images-specific attributes
    public function getContentAttribute($value){
        return $value;
    }

    public function images(){
        return $this->hasMany(PublicationImage::class);
    }
}
