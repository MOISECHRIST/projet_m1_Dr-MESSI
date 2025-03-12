<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Services\CommentService;

class CommentServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        $this->app->bind(CommentService::class, function ($app) {
            return new CommentService();
        });
    }

    /**
     * Bootstrap services.
     */
    public function boot(): void
    {
        //
    }
}
