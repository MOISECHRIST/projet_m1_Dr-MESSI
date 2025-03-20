<?php

namespace App\Http\Controllers;

use App\Services\CommentService;
use Illuminate\Http\Request;
use OpenApi\Annotations as OA;


class CommentController extends Controller
{
    protected $commentService;

    public function __construct(CommentService $commentService)
    {
        $this->commentService = $commentService;
    }



    /**
     * @OA\Post(
     *     path="/comments",
     *     summary="Créer un nouveau commentaire",
     *     tags={"Comments"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"user_id", "publication_id", "content"},
     *             @OA\Property(property="user_id", type="integer", example=1),
     *             @OA\Property(property="publication_id", type="integer", example=1),
     *             @OA\Property(property="content", type="string", example="Ceci est un commentaire.")
     *         ),
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Commentaire créé avec succès",
     *         @OA\JsonContent(ref="#/components/schemas/Comment")
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur de validation"
     *     ),
     * )
     */
    public function store(Request $request)
    {
        // Validation des données de la requête
        $request->validate([
            'user_id' => 'required|exists:users,id',
            'publication_id' => 'required|exists:publications,id',
            'content' => 'required|string',
        ]);

        try {
            // Création du commentaire
            $comment = $this->commentService->createComment(
                $request->input('user_id'),
                $request->input('publication_id'),
                $request->input('content')
            );

            return response()->json($comment, 201);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * @OA\Get(
     *     path="/comments/{commentId}",
     *     summary="Récupérer un commentaire par son ID",
     *     tags={"Comments"},
     *     @OA\Parameter(
     *         name="commentId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Détails du commentaire",
     *         @OA\JsonContent(ref="#/components/schemas/Comment")
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Commentaire non trouvé"
     *     ),
     * )
     */
    public function show($commentId)
    {
        try {
            $comment = $this->commentService->getComment($commentId);
            return response()->json($comment);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * @OA\Put(
     *     path="/comments/{commentId}",
     *     summary="Mettre à jour un commentaire",
     *     tags={"Comments"},
     *     @OA\Parameter(
     *         name="commentId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"content"},
     *             @OA\Property(property="content", type="string", example="Ceci est un commentaire mis à jour."),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Commentaire mis à jour avec succès",
     *         @OA\JsonContent(ref="#/components/schemas/Comment")
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur de validation"
     *     ),
     * )
     */
    public function update(Request $request, $commentId)
    {
        // Validation des données de la requête
        $request->validate([
            'content' => 'required|string',
        ]);

        try {
            // Mise à jour du commentaire
            $comment = $this->commentService->updateComment($commentId, $request->input('content'));
            return response()->json($comment);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * @OA\Delete(
     *     path="/comments/{commentId}",
     *     summary="Supprimer un commentaire",
     *     tags={"Comments"},
     *     @OA\Parameter(
     *         name="commentId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Commentaire supprimé avec succès"
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur lors de la suppression"
     *     ),
     * )
     */
    public function destroy($commentId)
    {
        try {
            $this->commentService->deleteComment($commentId);
            return response()->json(['message' => 'Commentaire supprimé avec succès']);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * @OA\Get(
     *     path="/publications/{publicationId}/comments",
     *     summary="Récupérer tous les commentaires d'une publication",
     *     tags={"Comments"},
     *     @OA\Parameter(
     *         name="publicationId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Liste des commentaires",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(ref="#/components/schemas/Comment")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Publication non trouvée"
     *     ),
     * )
     */
    public function getCommentsByPublication($publicationId)
    {
        try {
            $comments = $this->commentService->getCommentsByPublication($publicationId);
            return response()->json($comments);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * @OA\Get(
     *     path="/users/{userId}/comments",
     *     summary="Récupérer tous les commentaires d'un utilisateur",
     *     tags={"Comments"},
     *     @OA\Parameter(
     *         name="userId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Liste des commentaires",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(ref="#/components/schemas/Comment")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Utilisateur non trouvé"
     *     ),
     * )
     */
    public function getCommentsByUser($userId)
    {
        try {
            $comments = $this->commentService->getCommentsByUser($userId);
            return response()->json($comments);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }
}