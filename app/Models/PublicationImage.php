<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

/**
 * @OA\Schema(
 *     schema="PublicationImage",
 *     type="object",
 *     description="Représente une image associée à une publication",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="publication_id", type="integer", example=1),
 *     @OA\Property(property="image_path", type="string", example="public/publications/images/abc123.jpg"),
 *     @OA\Property(property="created_at", type="string", format="date-time", example="2023-10-01T12:00:00Z"),
 *     @OA\Property(property="updated_at", type="string", format="date-time", example="2023-10-01T12:00:00Z"),
 * )
 */
class PublicationImage extends Model
{
    protected $fillable = [
        'publication_id',
        'image_path',
    ];

    public function publication()
    {
        return $this->belongsTo(Publication::class);
    }

    /**
     * Accessor pour l'URL complète de l'image.
     *
     * @return string
     */
    public function getImageUrlAttribute():string
    {
        return asset('storage/' . $this->image_path);
    }
}
