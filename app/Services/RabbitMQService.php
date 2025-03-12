<?php

namespace App\Services;

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
use App\Models\User;
use Illuminate\Support\Facades\Log;

class RabbitMQService
{
    private $connection;
    private $channel;

    public function __construct()
    {
        $this->connection = new AMQPStreamConnection(
                                env('RABBITMQ_HOST'),
                                env('RABBITMQ_PORT'),
                                env('RABBITMQ_USER'),
                                env('RABBITMQ_PASSWORD')
                            );

        $this->channel = $this->connection->channel();
    }

    /**
     * Écouter les messages de connexion/déconnexion.
     */
    public function listenForAuthEvents()
    {
        $this->channel->queue_declare('auth_events', false, false, false, false);
        
        
        // Déclarer l'échange
        $this->channel->exchange_declare('auth_exchange', 'direct', false, true, false);


        // Lier la file d'attente à l'échange avec une clé de routage
        $this->channel->queue_bind('auth_events', 'auth_exchange', 'auth_event_key');
        
        
        $callback = function ($msg) {
            $data = json_decode($msg->body, true);

            $user = User::where('external_id', $data['user_id'])->first();

            if ($user) {
                if ($data['event'] === 'connected') {
                    $user->markAsConnected();
                    Log::info('User connected', ['user_id' => $user->id]);
                } elseif ($data['event'] === 'disconnected') {
                    $user->markAsDisconnected();
                    Log::info('User disconnected', ['user_id' => $user->id]);
                }
            }
        };

        $this->channel->basic_consume('auth_events', '', false, true, false, false, $callback);

        while ($this->channel->is_consuming()) {
            $this->channel->wait();
        }
    }

    public function __destruct()
    {
        $this->channel->close();
        $this->connection->close();
    }
}