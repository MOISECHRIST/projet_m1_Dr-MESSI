<?php

namespace App\Http\Controllers;

use App\Services\LikeService;
use Illuminate\Http\Request;

class LikeController extends Controller
{
    protected $likeService;

    public function __construct(LikeService $likeService)
    {
        $this->likeService = $likeService;
    }

    /**
     * Ajoute un "like" à une publication.
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function addLike(Request $request)
    {
        // Validation des données de la requête
        $request->validate([
            'user_id' => 'required|exists:users,id',
            'publication_id' => 'required|exists:publications,id',
            'rate' => 'required|integer|between:1,5', // Note entre 1 et 5
        ]);

        try {
            // Ajout du like
            $like = $this->likeService->addLike(
                $request->input('user_id'),
                $request->input('publication_id'),
                $request->input('rate')
            );

            return response()->json($like, 201);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Supprime un "like" d'une publication.
     *
     * @param int $likeId ID du like à supprimer
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function removeLike($likeId, Request $request)
    {
        // Validation des données de la requête
        $request->validate([
            'user_id' => 'required|exists:users,id',
        ]);

        try {
            // Suppression du like
            $this->likeService->removeLike($likeId, $request->input('user_id'));
            return response()->json(['message' => 'Like supprimé avec succès']);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Récupère tous les "likes" d'une publication.
     *
     * @param int $publicationId ID de la publication
     * @return \Illuminate\Http\JsonResponse
     */
    public function getLikesByPublication($publicationId)
    {
        try {
            $likes = $this->likeService->getLikesByPublication($publicationId);
            return response()->json($likes);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * Récupère tous les "likes" d'un utilisateur.
     *
     * @param int $userId ID de l'utilisateur
     * @return \Illuminate\Http\JsonResponse
     */
    public function getLikesByUser($userId)
    {
        try {
            $likes = $this->likeService->getLikesByUser($userId);
            return response()->json($likes);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * Met à jour un "like" existant.
     *
     * @param Request $request
     * @param int $likeId ID du like à mettre à jour
     * @return \Illuminate\Http\JsonResponse
     */
    public function updateLike(Request $request, $likeId)
    {
        // Validation des données de la requête
        $request->validate([
            'rate' => 'required|integer|between:1,5', // Note entre 1 et 5
        ]);

        try {
            // Mise à jour du like
            $like = $this->likeService->updateLike($likeId, $request->input('rate'));
            return response()->json($like);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Récupère un "like" spécifique par son ID.
     *
     * @param int $likeId ID du like
     * @return \Illuminate\Http\JsonResponse
     */
    public function getLikeById($likeId)
    {
        try {
            $like = $this->likeService->getLikeById($likeId);
            return response()->json($like);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * Calcule la moyenne des notes (rate) pour une publication donnée.
     *
     * @param int $publicationId ID de la publication
     * @return \Illuminate\Http\JsonResponse
     */
    public function getAverageRateForPublication($publicationId)
    {
        try {
            $averageRate = $this->likeService->getAverageRateForPublication($publicationId);

            if ($averageRate === null) {
                return response()->json(['message' => 'Aucun like trouvé pour cette publication.'], 404);
            }

            return response()->json(['average_rate' => $averageRate]);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }
}