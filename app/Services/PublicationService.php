<?php

namespace App\Services;

use App\Models\Publication;
use App\Models\TextImagePublication;
use App\Models\User;
use App\Models\VideoPublication;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\DB;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Str;

class PublicationService
{

    /**
     * Crée une nouvelle publication de type vidéo.
     *
     * @param int $userId ID de l'utilisateur (worker) qui crée la publication
     * @param string $video_url URL de la vidéo
     * @param string $title Titre de la publication
     * @param string|null $description Description de la publication
     * @return Publication
     * @throws \Exception Si l'utilisateur n'est pas un worker ou si la création échoue
     */
    public function createVideoPublication(int $userId, string $video_url, string $title, ?string $description = null): Publication
    {
        // Vérifier que l'utilisateur est un worker
        $this->validateWorker($userId);

        // Valider les données de la publication vidéo
        $validator = Validator::make([
            'video_url' => $video_url,
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
            $publication = new VideoPublication();
            $publication->user_id = $userId;
            $publication->title = $title;
            $publication->description = $description;
            $publication->video_url = $video_url;
            $publication->save();

            DB::commit();

            return $publication;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la création de la publication vidéo : ' . $e->getMessage());
            Log::error('Exception trace:', $e->getTrace());
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
    public function createTextWithImagesPublication(int $userId, string $content, string $title, ?string $description = null): Publication
    {
        // Vérifier que l'utilisateur est un worker
        $this->validateWorker($userId);

        // Valider les données de la publication texte + images
        $validator = Validator::make([
            'content' => $content,
            'title' => $title,
            'description' => $description,
        ], [
            'content' => 'required|string',
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            throw new \Exception('Données de publication texte + images invalides : ' . $validator->errors()->first());
        }

        DB::beginTransaction();

        try {
            $publication = new TextImagePublication();
            $publication->user_id = $userId;
            $publication->title = $title;
            $publication->description = $description;
            $publication->textContent = $content;
            $publication->type = 'TextImages';
            $publication->save();

            DB::commit();

            return $publication;
        } catch (\Exception $e) {
            DB::rollBack();
            Log::error('Erreur lors de la création de la publication texte + images : ' . $e->getMessage());
            Log::error('Exception trace:', $e->getTrace());
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
    public function getPublicationsByAuthor(int $authorId){
        $videoPublications = VideoPublication::with('user')->where('user_id', $authorId)->get();
        $textImagePublications = TextImagePublication::with('user', 'images')->where('user_id', $authorId)->get();

        // Transformer les publications pour inclure les URLs
        $videoPublications->transform(function ($publication) {
            return [
                'id' => $publication->id,
                'user_id' => $publication->user_id,
                'title' => $publication->title,
                'description' => $publication->description,
                'video_url' => asset('storage/' . $publication->video_path), // URL de la vidéo
                'type' => $publication->type, // Pour identifier le type de publication
                'created_at' => $publication->created_at,
                'updated_at' => $publication->updated_at,
                'nbr_view' => $publication->nbr_view
            ];
        });

        $textImagePublications->transform(function ($publication) {
            return [
                'id' => $publication->id,
                'user_id' => $publication->user_id,
                'title' => $publication->title,
                'description' => $publication->description,
                'textContent' => $publication->textContent,
                'images' => $publication->images->map(function ($image) {
                    return [
                        'id' => $image->id,
                        'image_url' => asset('storage/' . $image->image_path), // URL de l'image
                    ];
                }),
                'type' => 'TextImages', // Pour identifier le type de publication
                'created_at' => $publication->created_at,
                'updated_at' => $publication->updated_at,
            ];
        });

        // Combiner les deux types de publications
        $publications = $videoPublications->merge($textImagePublications);

        // Trier les publications par date de création (optionnel)
        $publications = $publications->sortByDesc('created_at')->values();


        return $publications;
    }

    /**
     * Mettre à jour une VideoPublication.
     */
    public  function updateVideoPublication(Request $request, $publication)
    {
        // Validation des données
        $request->validate([
            'title' => 'sometimes|string|max:255',
            'description' => 'nullable|string',
            'video' => 'sometimes|file|mimes:mp4,mov|max:102400', // 100MB max
        ]);

        // Mettre à jour les champs de base
        if ($request->has('title')) {
            $publication->title = $request->title;
        }
        if ($request->has('description')) {
            $publication->description = $request->description;
        }

        // Mettre à jour la vidéo si elle est fournie
        if ($request->hasFile('video')) {
            // Supprimer l'ancienne vidéo (optionnel)
            if ($publication->video_path) {
                Storage::delete('public/' . $publication->video_path);
            }

            // Sauvegarder la nouvelle vidéo
            $file = $request->file('video');
            $fileName = Str::uuid() . '.' . $file->getClientOriginalExtension();
            $filePath = $file->storeAs('publications/videos', $fileName, 'public');
            $publication->video_path = $filePath;
        }

        // Sauvegarder les modifications
        $publication->save();

        // Renvoyer la réponse JSON
        return response()->json([
            'message' => 'Publication vidéo mise à jour avec succès.',
            'publication' => $publication,
        ], 200);
    }

    /**
     * Mettre à jour une TextImagePublication.
     */
    public function updateTextImagePublication(Request $request, $publication)
    {
        // Validation des données
        $request->validate([
            'title' => 'sometimes|string|max:255',
            'description' => 'nullable|string',
            'images' => 'sometimes|array',
            'images.*' => 'image|mimes:jpeg,png,jpg,gif|max:2048', // 2MB max par image
        ]);

        // Mettre à jour les champs de base
        if ($request->has('title')) {
            $publication->title = $request->title;
        }
        if ($request->has('description')) {
            $publication->description = $request->description;
        }

        // Mettre à jour les images si elles sont fournies
        if ($request->has('images')) {
            // Supprimer les anciennes images (optionnel)
            foreach ($publication->images as $image) {
                Storage::delete('public/' . $image->image_path);
                $image->delete();
            }

            // Sauvegarder les nouvelles images
            foreach ($request->file('images') as $image) {
                $fileName = Str::uuid() . '.' . $image->getClientOriginalExtension();
                $filePath = $image->storeAs('publications/images', $fileName, 'public');

                // Enregistrer la nouvelle image dans la base de données
                $publication->images()->create([
                    'image_path' => $filePath,
                ]);
            }
        }

        // Sauvegarder les modifications
        $publication->save();

        // Renvoyer la réponse JSON
        return response()->json([
            'message' => 'Publication texte/images mise à jour avec succès.',
            'publication' => $publication,
        ], 200);
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
        $videoPublication = VideoPublication::with('user')->where('publication_id', $pubId)->get();
        $textImagePublication = TextImagePublication::with('user', 'images')->where('publication_id', $pubId)->get();

        if($videoPublication){
            // Transformer les publications pour inclure les URLs
            $videoPublication->transform(function ($publication) {
                return [
                    'id' => $publication->id,
                    'user_id' => $publication->user_id,
                    'title' => $publication->title,
                    'description' => $publication->description,
                    'video_url' => asset('storage/' . $publication->video_path), // URL de la vidéo
                    'type' => $publication->type, // Pour identifier le type de publication
                    'created_at' => $publication->created_at,
                    'updated_at' => $publication->updated_at,
                    'nbr_view' => $publication->nbr_view
                ];
            });
            $publication = $videoPublication;
        }
        else{
            $textImagePublication->transform(function ($publication) {
                return [
                    'id' => $publication->id,
                    'user_id' => $publication->user_id,
                    'title' => $publication->title,
                    'description' => $publication->description,
                    'textContent' => $publication->textContent,
                    'images' => $publication->images->map(function ($image) {
                        return [
                            'id' => $image->id,
                            'image_url' => asset('storage/' . $image->image_path), // URL de l'image
                        ];
                    }),
                    'type' => 'TextImages', // Pour identifier le type de publication
                    'created_at' => $publication->created_at,
                    'updated_at' => $publication->updated_at,
                ];
            });
            $publication = $textImagePublication;
        }

        return $publication;
    }

    public function getAllPublications(){
        // Récupérer toutes les publications (vidéos et textes/images)
        $videoPublications = VideoPublication::with('user')->get();
        $textImagePublications = TextImagePublication::with('user', 'images')->get();

        // Transformer les publications pour inclure les URLs
        $videoPublications->transform(function ($publication) {
            return [
                'id' => $publication->id,
                'user_id' => $publication->user_id,
                'title' => $publication->title,
                'description' => $publication->description,
                'video_url' => asset('storage/' . $publication->video_path), // URL de la vidéo
                'type' => $publication->type, // Pour identifier le type de publication
                'created_at' => $publication->created_at,
                'updated_at' => $publication->updated_at,
                'nbr_view' => $publication->nbr_view
            ];
        });

        $textImagePublications->transform(function ($publication) {
            return [
                'id' => $publication->id,
                'user_id' => $publication->user_id,
                'title' => $publication->title,
                'description' => $publication->description,
                'textContent' => $publication->textContent,
                'images' => $publication->images->map(function ($image) {
                    return [
                        'id' => $image->id,
                        'image_url' => asset('storage/' . $image->image_path), // URL de l'image
                    ];
                }),
                'type' => 'TextImages', // Pour identifier le type de publication
                'created_at' => $publication->created_at,
                'updated_at' => $publication->updated_at,
            ];
        });

        // Combiner les deux types de publications
        $publications = $videoPublications->merge($textImagePublications);

        // Trier les publications par date de création (optionnel)
        $publications = $publications->sortByDesc('created_at')->values();



        return $publications;
    }

    public function generateStreamUrl($publication){
        if($publication->video_url){
            $publication->stream_url = route('video.stream', ['filename'=> basename($publication->video_url)]);
        }
        return $publication;
    }
}


