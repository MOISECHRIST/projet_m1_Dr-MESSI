<?php

namespace App\Services;

use App\Models\Comment;
use App\Models\Publication;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;

class CommentService
{
    
    /**
     * Crée un nouveau commentaire.
     *
     * @param int $userId ID de l'utilisateur qui crée le commentaire
     * @param int $publicationId ID de la publication associée
     * @param string $content Contenu du commentaire
     * @return Comment
     * @throws \Exception Si la création échoue
     */
    public function createComment(int $userId, int $publicationId, string $content): Comment
    {
        DB::beginTransaction();

        try {
            // Vérifier que l'utilisateur et la publication existent
            $user = User::findOrFail($userId);
            $publication = Publication::findOrFail($publicationId);

            // Créer le commentaire
            $comment = new Comment();
            $comment->user_id = $userId;
            $comment->publication_id = $publicationId;
            $comment->content = $content;
            $comment->save();

            DB::commit();

            return $comment;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la création du commentaire : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la création du commentaire.');
        }
    }

    /**
     * Récupère un commentaire par son ID.
     *
     * @param int $commentId ID du commentaire
     * @return Comment
     * @throws \Exception Si le commentaire n'est pas trouvé
     */
    public function getComment(int $commentId): Comment
    {
        $comment = Comment::find($commentId);

        if (!$comment) {
            throw new \Exception('Commentaire non trouvé.');
        }

        return $comment;
    }

    /**
     * Met à jour un commentaire.
     *
     * @param int $commentId ID du commentaire
     * @param string $content Nouveau contenu du commentaire
     * @return Comment
     * @throws \Exception Si la mise à jour échoue
     */
    public function updateComment(int $commentId, string $content): Comment
    {
        DB::beginTransaction();

        try {
            $comment = Comment::findOrFail($commentId);
            $comment->content = $content;
            $comment->save();

            DB::commit();

            return $comment;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la mise à jour du commentaire : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la mise à jour du commentaire.');
        }
    }

    /**
     * Supprime un commentaire.
     *
     * @param int $commentId ID du commentaire
     * @return void
     * @throws \Exception Si la suppression échoue
     */
    public function deleteComment(int $commentId): void
    {
        DB::beginTransaction();

        try {
            $comment = Comment::findOrFail($commentId);
            $comment->delete();

            DB::commit();
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la suppression du commentaire : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la suppression du commentaire.');
        }
    }

    /**
     * Récupère tous les commentaires d'une publication.
     *
     * @param int $publicationId ID de la publication
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getCommentsByPublication(int $publicationId)
    {
        return Comment::where('publication_id', $publicationId)->get();
    }

    /**
     * Récupère tous les commentaires d'un utilisateur.
     *
     * @param int $userId ID de l'utilisateur
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getCommentsByUser(int $userId)
    {
        return Comment::where('user_id', $userId)->get();
    }
}