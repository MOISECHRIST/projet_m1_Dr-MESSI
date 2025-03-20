<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class VideoPublication extends Publication{

    protected $table = 'publications';


    protected $fillable = [
        'title',
        'description',
        'type',
        'user_id',

        'video_url',
        'nbr_view'
    ];


    protected static function boot()
    {
        parent::boot();

        // Set the type to 'video' when creating a new VideoPublication
        static::creating(function ($model) {
            $model->type = 'Video';
        });
    }

    /**
     * Accessor pour l'URL complète de la vidéo.
     *
     * @return string
     */
    public function getVideoUrlAttribute($value)
    {
        return asset('storage/' . $value); // Génère l'URL complète
    }

    // Accessor for nbr_view
    public function getNbrViewAttribute($value)
    {
        return $value;
    }


}
