<?php

namespace App\Providers;

use App\Services\LikeService;
use Illuminate\Support\ServiceProvider;

class LikeServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        $this->app->bind(LikeService::class, function ($app) {
            return new LikeService();
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
