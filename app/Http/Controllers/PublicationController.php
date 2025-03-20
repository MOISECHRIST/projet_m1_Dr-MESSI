<?php

namespace App\Http\Controllers;


use App\Models\Publication;
use App\Models\PublicationImage;
use App\Services\PublicationService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Log;
use Illuminate\Support\Facades\Storage;
use Illuminate\Support\Facades\Validator;
use Illuminate\Support\Str;
use OpenApi\Annotations as OA;
use Symfony\Component\HttpFoundation\StreamedResponse;

/**
 * @OA\Info(
 *     title="Publication API",
 *     version="1.0.0",
 *     description="API pour gérer les publications (texte, images et vidéos) les commentaires et les likes"
 * )
 * @OA\Server(
 *     url="http://localhost:8000/api",
 *     description="Server local"
 * )
 */
class PublicationController extends Controller{
    protected $publicationService;

    public function __construct(PublicationService $publicationService)
    {
        $this->publicationService = $publicationService;
    }

    /**
     * @OA\Post(
     *     path="/publications/video",
     *     summary="Créer une publication de type vidéo",
     *     tags={"Publications"},
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\MediaType(
     *             mediaType="multipart/form-data",
     *             @OA\Schema(
     *                  required={"user_id", "video_file", "title"},
     *                 @OA\Property(property="user_id", type="integer", example=1, description="ID de l'utilisateur qui cree la publication"),
     *                 @OA\Property(property="video_file", type="string", format="binary", description="Fichier a uploader"),
     *                 @OA\Property(property="title", type="string", example="Titre de la publication"),
     *                 @OA\Property(property="description", type="string", example="Description de la publication"),
     *             )
     *         ),
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Publication vidéo créée avec succès",
     *         @OA\JsonContent(ref="#/components/schemas/Publication")
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur de validation"
     *     ),
     * )
     */
    public function createVideoPublication(Request $request)
    {
        Log::info('Request data:', $request->all());
        Log::info('Request files:', $request->file());
        if ($request->hasFile('video_file')) {
            $file = $request->file('video_file');
            Log::info('File size:', ['size' => $file->getSize()]);
        } else {
            Log::error('No file uploaded or file upload failed.');
        }

        // Validation des données de la requête
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|exists:users,id',
            'video_file' => 'required|file|mimes:mov,mp4|max:102400', //100max
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);


        Log::info("Post validation pass");

        if ($validator->fails()) {
            Log::error('Validation errors:', $validator->errors()->toArray());
            return response()->json(['error' => $validator->errors()->first()], 400);
        }

        Log::info(" Second post validation pass");


        // Sauvegarder la video
        if($request->hasFile('video_file')){
            $file = $request->file('video_file');
            $fileName = Str::uuid() . '.' . $file->getClientOriginalExtension();
            $filePath = $file->storeAs('/publications/videos', $fileName, 'public');
        }
//            $filePath = 'b.mp4';
        try {
            // Création de la publication vidéo
            $publication = $this->publicationService->createVideoPublication(
                $request->user_id, // int $userId
                asset('storage/' . $filePath), // string $video_url
                $request->title, // string $title
                $request->description // ?string $description
            );
            return response()->json($publication, 201);
        } catch (\Exception $e) {
            Log::error('Erreur lors de l\'upload de la vidéo : ' . $e->getMessage());
            echo  $e->getMessage();
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }


    /**
     * @OA\Post(
     *     path="/publications/text-with-images",
     *     summary="Créer une publication de type texte avec images",
     *     description="Crée une publication contenant du texte et une ou plusieurs images. Les images doivent être au format JPEG, PNG, JPG ou GIF, avec une taille maximale de 2 Mo par image.",
     *     tags={"Publications"},
     *     @OA\RequestBody(
     *         required=true,
     *         description="Données nécessaires pour créer une publication texte + images",
     *         @OA\MediaType(
     *             mediaType="multipart/form-data",
     *             @OA\Schema(
     *                 required={"user_id", "content", "images", "title"},
     *                 @OA\Property(property="user_id", type="integer", example=1, description="ID de l'utilisateur créant la publication"),
     *                 @OA\Property(property="content", type="string", example="Contenu textuel de la publication", description="Contenu principal de la publication"),
     *                 @OA\Property(property="images", type="array", @OA\Items(type="string", format="binary"), description="Liste des images à associer à la publication"),
     *                 @OA\Property(property="title", type="string", example="Titre de la publication", description="Titre de la publication"),
     *                 @OA\Property(property="description", type="string", example="Description de la publication", description="Description optionnelle de la publication"),
     *             ),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=201,
     *         description="Publication texte + images créée avec succès",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="message", type="string", example="Publication créée avec succès"),
     *             @OA\Property(property="publication", ref="#/components/schemas/Publication"),
     *             @OA\Property(property="images", type="array", @OA\Items(ref="#/components/schemas/PublicationImage")),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur de validation ou autre erreur",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="error", type="string", example="Une erreur s'est produite lors de la création de la publication."),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=500,
     *         description="Erreur serveur interne",
     *         @OA\JsonContent(
     *             type="object",
     *             @OA\Property(property="error", type="string", example="Erreur serveur interne"),
     *         ),
     *     ),
     * )
     */
    public function createTextWithImagesPublication(Request $request)
    {
        Log::info('Request data:', $request->all());
        Log::info('Request files:', $request->file());
        // Validation des données de la requête
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|exists:users,id',
            'content' => 'required|string',
            'images.*' => 'image|mimes:jpeg,png,jpg,gif|max:2048', // 2MB max par image
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => $validator->errors()->first()], 400);
        }

        try {
            // Création de la publication texte + images
            $publication = $this->publicationService->createTextWithImagesPublication(
                $request->input('user_id'),
                $request->input('content'),
                $request->input('title'),
                $request->input('description')
            );

        Log::info("Pretraitement des images");
        // Traiter chaque image
        if ($request->hasFile('images')) {
            foreach ($request->file('images') as $image) {
                $fileName = Str::uuid() . '.' . $image->getClientOriginalExtension();
                $filePath = $image->storeAs('/publications/images', $fileName, 'public');
                Log::info("Traitement des images");
                // Enregistrer l'image dans la table post_images
                PublicationImage::create([
                    'publication_id' => $publication->id,
                    'image_path' => $filePath,
                ]);

                Log::info("Post traitement des images");
            }
        }


            return response()->json(['message'=>'Publication cree avec succes',
                                    'publication'=>$publication,
                                    'images' => $publication->images], 201);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * @OA\Get(
     *     path="/publications/author/{authorId}",
     *     summary="Récupérer toutes les publications d'un auteur",
     *     tags={"Publications"},
     *     @OA\Parameter(
     *         name="authorId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Liste des publications de l'auteur",
     *         @OA\JsonContent(
     *             type="array",
     *             @OA\Items(ref="#/components/schemas/Publication")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Auteur non trouvé"
     *     ),
     * )
     */
    public function getPublicationsByAuthor($authorId)
    {
        try {
            $publications = $this->publicationService->getPublicationsByAuthor($authorId);

            $publications->transform(
                function($publication) {
                    return $this->publicationService->generateStreamUrl($publication);
            });

            return response()->json($publications);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * @OA\Get(
     *     path="/publications/{pubId}",
     *     summary="Récupérer une publication par son ID",
     *     tags={"Publications"},
     *     @OA\Parameter(
     *         name="pubId",
     *         in="path",
     *         required=true,
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Détails de la publication",
     *         @OA\JsonContent(ref="#/components/schemas/Publication")
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Publication non trouvée"
     *     ),
     * )
     */
    public function getPublicationById($pubId)
    {
        try {
            $publication = $this->publicationService->getPublicationById($pubId);
            $publication = $this->publicationService->generateStreamUrl($publication);
            return response()->json($publication);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * @OA\Delete(
     *     path="/publications/{pubId}",
     *     summary="Supprimer une publication",
     *     tags={"Publications"},
     *     @OA\Parameter(
     *         name="pubId",
     *         in="path",
     *         required=true,
     *         description="ID de la publication à supprimer",
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\JsonContent(
     *             required={"user_id"},
     *             @OA\Property(property="user_id", type="integer", example=1, description="ID de l'utilisateur qui demande la suppression"),
     *         ),
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Publication supprimée avec succès",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Publication supprimée avec succès.")
     *         )
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur lors de la suppression",
     *         @OA\JsonContent(
     *             @OA\Property(property="error", type="string", example="Message d'erreur")
     *         )
     *     ),
     *     @OA\Response(
     *         response=403,
     *         description="Accès refusé (l'utilisateur n'est pas l'auteur de la publication)",
     *         @OA\JsonContent(
     *             @OA\Property(property="error", type="string", example="Vous n'êtes pas autorisé à supprimer cette publication.")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Publication non trouvée",
     *         @OA\JsonContent(
     *             @OA\Property(property="error", type="string", example="Publication non trouvée.")
     *         )
     *     )
     * )
     */
    public function deletePublication(Request $request, $pubId)
    {
        // Validation des données de la requête
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|exists:users,id',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => $validator->errors()->first()], 400);
        }

        try {
            // Récupérer la publication
            $publication = Publication::find($pubId);

            // Vérifier si la publication existe
            if (!$publication) {
                return response()->json(['error' => 'Publication non trouvée.'], 404);
            }

            // Vérifier si l'utilisateur est l'auteur de la publication
            if ($publication->user_id != $request->input('user_id')) {
                return response()->json(['error' => 'Vous n\'êtes pas autorisé à supprimer cette publication.'], 403);
            }

            // Supprimer les fichiers multimédias associés
            if ($publication->type === 'Video' && $publication->video_path) {
                Storage::delete('public/' . $publication->video_path);
            } elseif ($publication->type === 'TextImages') {
                foreach ($publication->images as $image) {
                    Storage::delete('public/' . $image->image_path);
                    $image->delete(); // Supprimer l'entrée de la base de données
                }
            }

            // Supprimer la publication
            $publication->delete();

            return response()->json(['message' => 'Publication supprimée avec succès.'], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }


    /**
     * @OA\Get(
     *     path="/publications",
     *     summary="Récupérer toutes les publications",
     *     tags={"Publications"},
     *     @OA\Response(
     *         response=200,
     *         description="Liste des publications",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Publications récupérées avec succès."),
     *              @OA\Property(
     *                  property="publications",
     *                  type="array",
     *                  @OA\Items(ref="#/components/schemas/Publication")
     *              )
     *         )
     *     ),
     *     @OA\Response(
     *         response=500,
     *         description="Erreur serveur"
     *     ),
     * )
     */
    public function getAllPublications()
    {
        try {

            $publications = $this->publicationService->getAllPublications();

            // Ajouter l'URL de streaming pour chaque post contenant une video
            $publications->transform(
                function($publication) {
                    return $this->publicationService->generateStreamUrl($publication);
                }
            );


            return response()->json(['message'=>'Publications recuperes avec succes', $publications], 200);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }


    /**
     * @OA\Get(
     *     path="/publications/video/{filename}",
     *     summary="Streamer une vidéo",
     *     tags={"Publications"},
     *     @OA\Parameter(
     *         name="filename",
     *         in="path",
     *         required=true,
     *         description="Nom du fichier vidéo",
     *         @OA\Schema(type="string")
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Vidéo streamée avec succès",
     *         @OA\MediaType(
     *             mediaType="video/mp4",
     *             @OA\Schema(type="string", format="binary")
     *         )
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Vidéo non trouvée"
     *     )
     * )
     */
    public function streamVideo($filename)
    {
        $path = storage_path('app/public/publications/videos/' . $filename);

        if (!file_exists($path)) {
            return response()->json(['message' => 'Vidéo non trouvée.'], 404);
        }

        // Streamer la vidéo
        $stream = new StreamedResponse(function() use ($path) {
            $stream = fopen($path, 'rb');
            fpassthru($stream);
            fclose($stream);
        });

        $stream->headers->set('Content-Type', mime_content_type($path));
        $stream->headers->set('Content-Disposition', 'inline; filename="' . $filename . '"');

        return $stream;
    }




    /**
     * @OA\Put(
     *     path="/publications/{id}",
     *     summary="Mettre à jour une publication",
     *     tags={"Publications"},
     *     @OA\Parameter(
     *         name="id",
     *         in="path",
     *         required=true,
     *         description="ID de la publication à mettre à jour",
     *         @OA\Schema(type="integer")
     *     ),
     *     @OA\RequestBody(
     *         required=true,
     *         @OA\MediaType(
     *             mediaType="multipart/form-data",
     *             @OA\Schema(
     *                 @OA\Property(
     *                     property="title",
     *                     type="string",
     *                     example="Nouveau titre",
     *                     description="Titre de la publication"
     *                 ),
     *                 @OA\Property(
     *                     property="description",
     *                     type="string",
     *                     example="Nouvelle description",
     *                     description="Description de la publication"
     *                 ),
     *                 @OA\Property(
     *                     property="video",
     *                     type="string",
     *                     format="binary",
     *                     description="Fichier vidéo à uploader (uniquement pour les publications vidéo)"
     *                 ),
     *                 @OA\Property(
     *                     property="images",
     *                     type="array",
     *                     @OA\Items(type="string", format="binary"),
     *                     description="Fichiers images à uploader (uniquement pour les publications texte/images)"
     *                 )
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=200,
     *         description="Publication mise à jour avec succès",
     *         @OA\JsonContent(
     *             @OA\Property(property="message", type="string", example="Publication mise à jour avec succès."),
     *             @OA\Property(
     *                 property="publication",
     *                 type="object",
     *                 ref="#/components/schemas/Publication"
     *             )
     *         )
     *     ),
     *     @OA\Response(
     *         response=400,
     *         description="Erreur de validation ou type de publication non supporté"
     *     ),
     *     @OA\Response(
     *         response=404,
     *         description="Publication non trouvée"
     *     )
     * )
     */
    public function update(Request $request, $id)
    {
        // Trouver la publication par son ID
        $publication = Publication::findOrFail($id);

        // Vérifier le type de publication
        if ($publication->type === 'Video') {
            // Mise à jour d'une VideoPublication
            return $this->publicationService->updateVideoPublication($request, $publication);
        } elseif ($publication->type === 'TextImages') {
            // Mise à jour d'une TextImagePublication
            return $this->publicationService->updateTextImagePublication($request, $publication);
        }

        // Si le type n'est pas reconnu
        return response()->json(['message' => 'Type de publication non supporté.'], 400);
    }


}
