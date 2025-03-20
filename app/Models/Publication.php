<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;


/**
 * @OA\Schema(
 *     schema="Publication",
 *     type="object",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="user_id", type="integer", example=1),
 *     @OA\Property(property="type", type="string", example="video"),
 *     @OA\Property(property="title", type="string", example="Titre de la publication"),
 *     @OA\Property(property="description", type="string", example="Description de la publication"),
 *     @OA\Property(property="video_url", type="string", format="url", example="https://example.com/video.mp4"),
 *     @OA\Property(property="content", type="string", example="Contenu textuel de la publication"),
 *     @OA\Property(property="images", type="array", @OA\Items(type="string", format="url")),
 *     @OA\Property(property="created_at", type="string", format="date-time"),
 *     @OA\Property(property="updated_at", type="string", format="date-time"),
 * )
 */
class Publication extends Model{

    /**
     * @var mixed|string
     */
    protected $table = 'publications';

    protected $fillable = [
        'user_id',
        'title',
        'description',
        'type',
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

    
    public function images()
    {
        return $this->hasMany(PublicationImage::class, 'publication_id');
    }


}
