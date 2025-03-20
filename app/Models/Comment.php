<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Model;
use App\Models\User; // Assurez-vous que cette ligne est présente
use App\Models\Publication; // Assurez-vous que cette ligne est présente

/**
 * @OA\Schema(
 *     schema="Comment",
 *     type="object",
 *     description="Représente un commentaire",
 *     @OA\Property(property="id", type="integer", example=1),
 *     @OA\Property(property="content", type="string", example="Ceci est un commentaire"),
 *     @OA\Property(property="user_id", type="integer", example=1),
 *     @OA\Property(property="publication_id", type="integer", example=1),
 *     @OA\Property(property="created_at", type="string", format="date-time", example="2023-10-01T12:00:00Z"),
 *     @OA\Property(property="updated_at", type="string", format="date-time", example="2023-10-01T12:00:00Z")
 * )
 */
class Comment extends Model
{
    use HasFactory; // Utilisez le trait HasFactory si nécessaire

    protected $fillable = [
        'user_id',
        'publication_id',
        'content',
    ];

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function publication(): BelongsTo
    {
        return $this->belongsTo(Publication::class);
    }
}