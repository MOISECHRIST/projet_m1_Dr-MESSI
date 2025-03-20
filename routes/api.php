<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\PublicationController;
use App\Http\Controllers\CommentController;
use App\Http\Controllers\LikeController;

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

//Route::middleware('auth:sanctum')->get('/user', function (Request $request) {
//    return $request->user();
//});


Route::post('/publications/video', [PublicationController::class, 'createVideoPublication']);
Route::post('/publications/text-with-images', [PublicationController::class, 'createTextWithImagesPublication']);
Route::get('/publications/author/{authorId}', [PublicationController::class, 'getPublicationsByAuthor']);
Route::get('/publications/{pubId}', [PublicationController::class, 'getPublicationById']);
Route::put('/publications/{pubId}', [PublicationController::class, 'updatePublication']);
Route::delete('/publications/{pubId}', [PublicationController::class, 'deletePublication']);
Route::get('/publications', [PublicationController::class, 'getAllPublications']);
Route::get('/publications/video/{filename}', [PublicationController::class, 'streamVideo'])->name('video.stream');



Route::post('/comments', [CommentController::class, 'store']);
Route::get('/comments/{commentId}', [CommentController::class, 'show']);
Route::put('/comments/{commentId}', [CommentController::class, 'update']);
Route::delete('/comments/{commentId}', [CommentController::class, 'destroy']);
Route::get('/publications/{publicationId}/comments', [CommentController::class, 'getCommentsByPublication']);
Route::get('/users/{userId}/comments', [CommentController::class, 'getCommentsByUser']);



Route::post('/likes', [LikeController::class, 'addLike']);
Route::delete('/likes/{likeId}', [LikeController::class, 'removeLike']);
Route::get('/publications/{publicationId}/likes', [LikeController::class, 'getLikesByPublication']);
Route::get('/users/{userId}/likes', [LikeController::class, 'getLikesByUser']);
Route::put('/likes/{likeId}', [LikeController::class, 'updateLike']);
Route::get('/likes/{likeId}', [LikeController::class, 'getLikeById']);
Route::get('/publications/{publicationId}/average-rate', [LikeController::class, 'getAverageRateForPublication']);


