<?php

namespace App\Http\Controllers;

use App\Services\CommentService;
use Illuminate\Http\Request;

class CommentController extends Controller
{
    protected $commentService;

    public function __construct(CommentService $commentService)
    {
        $this->commentService = $commentService;
    }

    /**
     * Crée un nouveau commentaire.
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
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
     * Récupère un commentaire par son ID.
     *
     * @param int $commentId ID du commentaire
     * @return \Illuminate\Http\JsonResponse
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
     * Met à jour un commentaire existant.
     *
     * @param Request $request
     * @param int $commentId ID du commentaire à mettre à jour
     * @return \Illuminate\Http\JsonResponse
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
     * Supprime un commentaire.
     *
     * @param int $commentId ID du commentaire à supprimer
     * @return \Illuminate\Http\JsonResponse
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
     * Récupère tous les commentaires d'une publication.
     *
     * @param int $publicationId ID de la publication
     * @return \Illuminate\Http\JsonResponse
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
     * Récupère tous les commentaires d'un utilisateur.
     *
     * @param int $userId ID de l'utilisateur
     * @return \Illuminate\Http\JsonResponse
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