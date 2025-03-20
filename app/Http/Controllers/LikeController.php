<?php

namespace App\Http\Controllers;

use App\Services\LikeService;
use Illuminate\Http\Request;
use OpenApi\Annotations as OA;


class LikeController extends Controller
{
    protected $likeService;

    public function __construct(LikeService $likeService)
    {
        $this->likeService = $likeService;
    }

    /**
     * @OA\Post(
     *     path="/likes",
     *     summary="Ajouter un like",
     *     tags={"Likes"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"user_id", "publication_id", "rate"},
     *             @OA\Property(property="user_id", type="integer", example=1),
     *             @OA\Property(property="publication_id", type="integer", example=1),
     *             @OA\Property(property="rate", type="integer", example=4),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Like ajouté avec succès",
     *         @OA\JsonContent(ref="#/components/schemas/Like")
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur de validation"
     *     ),
     * )
     */
    public function addLike(Request $request)
    {
        $request->validate([
            'user_id' => 'required|exists:users,id',
            'publication_id' => 'required|exists:publications,id',
            'rate' => 'required|integer|between:1,5',
        ]);

        try {
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
     * @OA\Delete(
     *     path="/likes/{likeId}",
     *     summary="Supprimer un like",
     *     tags={"Likes"},
     *     @OA\Parameter(
     *         name="likeId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"user_id"},
     *             @OA\Property(property="user_id", type="integer", example=1),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Like supprimé avec succès"
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur lors de la suppression"
     *     ),
     * )
     */
    public function removeLike($likeId, Request $request)
    {
        $request->validate([
            'user_id' => 'required|exists:users,id',
        ]);

        try {
            $this->likeService->removeLike($likeId, $request->input('user_id'));
            return response()->json(['message' => 'Like supprimé avec succès']);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * @OA\Get(
     *     path="/publications/{publicationId}/likes",
     *     summary="Récupérer les likes d'une publication",
     *     tags={"Likes"},
     *     @OA\Parameter(
     *         name="publicationId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Liste des likes",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(ref="#/components/schemas/Like")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Publication non trouvée"
     *     ),
     * )
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
     * @OA\Get(
     *     path="/users/{userId}/likes",
     *     summary="Récupérer les likes d'un utilisateur",
     *     tags={"Likes"},
     *     @OA\Parameter(
     *         name="userId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Liste des likes",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(ref="#/components/schemas/Like")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Utilisateur non trouvé"
     *     ),
     * )
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
     * @OA\Put(
     *     path="/likes/{likeId}",
     *     summary="Mettre à jour un like",
     *     tags={"Likes"},
     *     @OA\Parameter(
     *         name="likeId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"rate"},
     *             @OA\Property(property="rate", type="integer", example=5),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Like mis à jour avec succès",
     *         @OA\JsonContent(ref="#/components/schemas/Like")
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur lors de la mise à jour"
     *     ),
     * )
     */
    public function updateLike(Request $request, $likeId)
    {
        $request->validate([
            'rate' => 'required|integer|between:1,5',
        ]);

        try {
            $like = $this->likeService->updateLike($likeId, $request->input('rate'));
            return response()->json($like);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * @OA\Get(
     *     path="/likes/{likeId}",
     *     summary="Récupérer un like par son ID",
     *     tags={"Likes"},
     *     @OA\Parameter(
     *         name="likeId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Détails du like",
     *         @OA\JsonContent(ref="#/components/schemas/Like")
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Like non trouvé"
     *     ),
     * )
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
     * @OA\Get(
     *     path="/publications/{publicationId}/average-rate",
     *     summary="Récupérer la moyenne des notes d'une publication",
     *     tags={"Likes"},
     *     @OA\Parameter(
     *         name="publicationId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Moyenne des notes",
     *         @OA\JsonContent(
     *             @OA\Property(property="average_rate", type="number", example=4.5)
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Aucun like trouvé pour cette publication"
     *     ),
     * )
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