<?php

namespace App\Http\Controllers;

use App\Services\PublicationService;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Validator;

class PublicationController extends Controller
{
    protected $publicationService;

    public function __construct(PublicationService $publicationService)
    {
        $this->publicationService = $publicationService;
    }

    /**
     * Crée une nouvelle publication de type vidéo.
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function createVideoPublication(Request $request)
    {
        // Validation des données de la requête
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|exists:users,id',
            'video_url' => 'required|url',
            'title' => 'required|string|max:255',
            'description' => 'nullable|string',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => $validator->errors()->first()], 400);
        }

        try {
            // Création de la publication vidéo
            $publication = $this->publicationService->createVideoPublication(
                $request->input('user_id'),
                $request->input('video_url'),
                $request->input('title'),
                $request->input('description')
            );

            return response()->json($publication, 201);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Crée une nouvelle publication de type texte + images.
     *
     * @param Request $request
     * @return \Illuminate\Http\JsonResponse
     */
    public function createTextWithImagesPublication(Request $request)
    {
        // Validation des données de la requête
        $validator = Validator::make($request->all(), [
            'user_id' => 'required|exists:users,id',
            'content' => 'required|string',
            'images' => 'required|array',
            'images.*' => 'url',
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
                $request->input('images'),
                $request->input('title'),
                $request->input('description')
            );

            return response()->json($publication, 201);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Récupère toutes les publications d'un auteur.
     *
     * @param int $authorId ID de l'auteur
     * @return \Illuminate\Http\JsonResponse
     */
    public function getPublicationsByAuthor($authorId)
    {
        try {
            $publications = $this->publicationService->getPublicationsByAuthor($authorId);
            return response()->json($publications);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * Récupère une publication spécifique par son ID.
     *
     * @param int $pubId ID de la publication
     * @return \Illuminate\Http\JsonResponse
     */
    public function getPublicationById($pubId)
    {
        try {
            $publication = $this->publicationService->getPublicationById($pubId);
            return response()->json($publication);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 404);
        }
    }

    /**
     * Met à jour une publication existante.
     *
     * @param Request $request
     * @param int $pubId ID de la publication à mettre à jour
     * @return \Illuminate\Http\JsonResponse
     */
    public function updatePublication(Request $request, $pubId)
    {
        // Validation des données de la requête
        $validator = Validator::make($request->all(), [
            'title' => 'sometimes|string|max:255',
            'description' => 'nullable|string',
            'video_url' => 'sometimes|url',
            'content' => 'sometimes|string',
            'images' => 'sometimes|array',
            'images.*' => 'url',
        ]);

        if ($validator->fails()) {
            return response()->json(['error' => $validator->errors()->first()], 400);
        }

        try {
            // Mise à jour de la publication
            $publication = $this->publicationService->updatePublication($pubId, $request->all());
            return response()->json($publication);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Supprime une publication.
     *
     * @param Request $request
     * @param int $pubId ID de la publication à supprimer
     * @return \Illuminate\Http\JsonResponse
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
            // Suppression de la publication
            $this->publicationService->deletePublication($pubId, $request->input('user_id'));
            return response()->json(['message' => 'Publication supprimée avec succès']);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 400);
        }
    }

    /**
     * Récupère toutes les publications.
     *
     * @return \Illuminate\Http\JsonResponse
     */
    public function getAllPublications()
    {
        try {
            $publications = $this->publicationService->getAllPublications();
            return response()->json($publications);
        } catch (\Exception $e) {
            return response()->json(['error' => $e->getMessage()], 500);
        }
    }
}