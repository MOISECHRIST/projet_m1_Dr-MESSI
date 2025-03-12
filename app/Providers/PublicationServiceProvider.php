<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Services\PublicationService;

class PublicationServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        $this->app->bind(PublicationService::class, function ($app) {
            return new PublicationService();
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
