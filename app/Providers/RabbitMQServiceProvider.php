<?php

namespace App\Providers;

use App\Services\RabbitMQService;
use Illuminate\Support\ServiceProvider;
use App\Services\UserService;

class RabbitMQServiceProvider extends ServiceProvider
{
    /**
     * Register services.
     */
    public function register(): void
    {
        $this->app->singleton(RabbitMQService::class, function ($app) {
            return new RabbitMQService($app->make(UserService::class));
        });
    }

    /**
     * Bootstrap services.
     */
    public function boot(): void
    {

        if (env('RABBITMQ_ENABLED', true) === true) {
            $rabbitService = app(RabbitMQService::class);
            $rabbitService->listenForUserEvents();
        }

       
    }
}
