<?php

namespace App\Services;

use App\Models\Like;
use App\Models\Publication;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class LikeService
{
     /**
     * Ajoute un "like" à une publication.
     *
     * @param int $userId ID de l'utilisateur qui like la publication
     * @param int $publicationId ID de la publication likée
     * @param int $rate Note du like (par exemple, 1 pour like, -1 pour dislike)
     * @return Like
     * @throws \Exception Si l'utilisateur ou la publication n'existe pas, ou si le like échoue
     */
    public function addLike(int $userId, int $publicationId, int $rate): Like
    {
        // Vérifier que l'utilisateur et la publication existent
        $user = User::findOrFail($userId);
        $publication = Publication::findOrFail($publicationId);
    
        DB::beginTransaction();
    
        try {
            // Vérifier si un like existe déjà pour cet utilisateur et cette publication
            $like = Like::updateOrCreate(
                [
                    'user_id' => $userId,
                    'publication_id' => $publicationId,
                ],
                [
                    'rate' => $rate,
                ]
            );
    
            DB::commit();
    
            return $like;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de l\'ajout du like : ' . $e->getMessage());
            throw new \Exception('Erreur lors de l\'ajout du like.');
        }
    }

    /**
     * Supprime un "like" d'une publication.
     *
     * @param int $likeId ID du like à supprimer
     * @param int $userId ID de l'utilisateur qui supprime le like
     * @return void
     * @throws \Exception Si le like n'existe pas ou si la suppression échoue
     */
    public function removeLike(int $likeId, int $userId): void
    {
        DB::beginTransaction();

        try {
            // Trouver le like et vérifier qu'il appartient à l'utilisateur
            $like = Like::where('id', $likeId)
                ->where('user_id', $userId)
                ->firstOrFail();

            $like->delete();

            DB::commit();
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la suppression du like : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la suppression du like.');
        }
    }

    /**
     * Récupère tous les "likes" d'une publication.
     *
     * @param int $publicationId ID de la publication
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getLikesByPublication(int $publicationId)
    {
        return Like::where('publication_id', $publicationId)->get();
    }

    /**
     * Récupère tous les "likes" d'un utilisateur.
     *
     * @param int $userId ID de l'utilisateur
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getLikesByUser(int $userId)
    {
        return Like::where('user_id', $userId)->get();
    }

    /**
     * Met à jour un "like" existant.
     *
     * @param int $likeId ID du like à mettre à jour
     * @param int $rate Nouvelle note du like
     * @return Like
     * @throws \Exception Si le like n'existe pas ou si la mise à jour échoue
     */
    public function updateLike(int $likeId, int $rate): Like
    {
        DB::beginTransaction();

        try {
            $like = Like::findOrFail($likeId);
            $like->rate = $rate;
            $like->save();

            DB::commit();

            return $like;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la mise à jour du like : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la mise à jour du like.');
        }
    }

    /**
     * Récupère un "like" spécifique par son ID.
     *
     * @param int $likeId ID du like
     * @return Like
     * @throws \Exception Si le like n'existe pas
     */
    public function getLikeById(int $likeId): Like
    {
        $like = Like::find($likeId);

        if (!$like) {
            throw new \Exception('Like non trouvé.');
        }

        return $like;
    }


    /**
     * Calcule la moyenne des notes (rate) pour une publication donnée.
     *
     * @param int $publicationId ID de la publication
     * @return float|null La moyenne des notes, ou null si aucun like n'existe
     */
    public function getAverageRateForPublication(int $publicationId): ?float
    {
        $likes = Like::where('publication_id', $publicationId)->get();

        if ($likes->isEmpty()) {
            return null;
        }

        $totalRate = $likes->sum('rate');

        $averageRate = $totalRate / $likes->count();

        return round($averageRate, 2);
    }
}