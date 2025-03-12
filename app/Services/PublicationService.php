<?php

namespace App\Services;

use App\Models\Publication;
use App\Models\User;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;

class PublicationService
{

    /**
     * Crée une nouvelle publication de type vidéo.
     *
     * @param int $userId ID de l'utilisateur (worker) qui crée la publication
     * @param string $videoUrl URL de la vidéo
     * @param string $title Titre de la publication
     * @param string|null $description Description de la publication
     * @return Publication
     * @throws \Exception Si l'utilisateur n'est pas un worker ou si la création échoue
     */
    public function createVideoPublication(int $userId, string $videoUrl, string $title, ?string $description = null): Publication
    {
        // Vérifier que l'utilisateur est un worker
        $this->validateWorker($userId);

        // Valider les données de la publication vidéo
        $validator = Validator::make([
            'video_url' => $videoUrl,
            'title' => $title,
            'description' => $description,
        ], [
            'video_url' => 'required|url',
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            throw new \Exception('Données de publication vidéo invalides : ' . $validator->errors()->first());
        }

        DB::beginTransaction();

        try {
            $publication = new Publication();
            $publication->user_id = $userId;
            $publication->type = 'video';
            $publication->title = $title;
            $publication->description = $description;
            $publication->video_url = $videoUrl;
            $publication->save();

            DB::commit();

            return $publication;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la création de la publication vidéo : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la création de la publication vidéo.');
        }
    }

    /**
     * Crée une nouvelle publication de type texte + images.
     *
     * @param int $userId ID de l'utilisateur (worker) qui crée la publication
     * @param string $content Contenu textuel de la publication
     * @param array $images URLs des images
     * @param string $title Titre de la publication
     * @param string|null $description Description de la publication
     * @return Publication
     * @throws \Exception Si l'utilisateur n'est pas un worker ou si la création échoue
     */
    public function createTextWithImagesPublication(int $userId, string $content, array $images, string $title, ?string $description = null): Publication
    {
        // Vérifier que l'utilisateur est un worker
        $this->validateWorker($userId);

        // Valider les données de la publication texte + images
        $validator = Validator::make([
            'content' => $content,
            'images' => $images,
            'title' => $title,
            'description' => $description,
        ], [
            'content' => 'required|string',
            'images' => 'required|array',
            'images.*' => 'url', // Valider chaque URL d'image
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            throw new \Exception('Données de publication texte + images invalides : ' . $validator->errors()->first());
        }

        DB::beginTransaction();

        try {
            $publication = new Publication();
            $publication->user_id = $userId;
            $publication->type = 'text_with_images';
            $publication->title = $title;
            $publication->description = $description;
            $publication->content = $content;
            $publication->images = json_encode($images); // Stocker les images sous forme de JSON
            $publication->save();

            DB::commit();

            return $publication;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la création de la publication texte + images : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la création de la publication texte + images.');
        }
    }

    /**
     * Vérifie que l'utilisateur est un worker.
     *
     * @param int $userId ID de l'utilisateur
     * @throws \Exception Si l'utilisateur n'est pas un worker
     */
    private function validateWorker(int $userId): void
    {
        $user = User::findOrFail($userId);
        if (!($user->role === 'worker')) {
            throw new \Exception('Seuls les workers peuvent créer des publications.');
        }
    }

    /**
     * Récupère toutes les publications d'un auteur.
     *
     * @param int $authorId ID de l'auteur
     * @return \Illuminate\Database\Eloquent\Collection
     */
    public function getPublicationsByAuthor(int $authorId)
    {
        return Publication::where('user_id', $authorId)->get();
    }

    /**
     * Met à jour une publication existante.
     *
     * @param int $pubId ID de la publication à mettre à jour
     * @param array $updatedData Données mises à jour
     * @return Publication
     * @throws \Exception Si la mise à jour échoue
     */
    public function updatePublication(int $pubId, array $updatedData): Publication
    {
        DB::beginTransaction();

        try {
            $publication = Publication::findOrFail($pubId);
            $publication->update($updatedData);
            DB::commit();

            return $publication;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la mise à jour de la publication : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la mise à jour de la publication.');
        }
    }

    /**
     * Supprime une publication.
     *
     * @param int $pubId ID de la publication à supprimer
     * @param int $userId ID de l'utilisateur (worker) qui supprime la publication
     * @return void
     * @throws \Exception Si l'utilisateur n'est pas un worker ou si la suppression échoue
     */
    public function deletePublication(int $pubId, int $userId): void
    {
        $this->validateWorker($userId);

        DB::beginTransaction();

        try {
            $publication = Publication::findOrFail($pubId);
            $publication->delete();
            DB::commit();
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la suppression de la publication : ' . $e->getMessage());
            throw new \Exception('Erreur lors de la suppression de la publication.');
        }
    }

    public function getPublicationById(int $pubId){
        return Publication::where('publication_id', $pubId);
    }


    public function getAllPublications(){
        return Publication::all();
    }
}