<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PublicationController;

/*
|--------------------------------------------------------------------------
| API Routes
|--------------------------------------------------------------------------
|
| Here is where you can register API routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "api" middleware group. Make something great!
|
*/

Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
    return $request->user();
});



Route::post('/publications/video', [PublicationController::class, 'createVideoPublication']);
Route::post('/publications/text-with-images', [PublicationController::class, 'createTextWithImagesPublication']);
Route::get('/publications/author/{authorId}', [PublicationController::class, 'getPublicationsByAuthor']);
Route::get('/publications/{pubId}', [PublicationController::class, 'getPublicationById']);
Route::put('/publications/{pubId}', [PublicationController::class, 'updatePublication']);
Route::delete('/publications/{pubId}', [PublicationController::class, 'deletePublication']);
Route::get('/publications', [PublicationController::class, 'getAllPublications']);