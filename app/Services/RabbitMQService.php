<?php

namespace App\Services;

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;
use App\Services\UserService;
use Illuminate\Support\Facades\Log;

class RabbitMQService
{
    private $connection;
    private $channel;
    private $userService;

    // Types d'événements utilisateur
    const EVENT_CONNECTED = 'connected';
    const EVENT_DISCONNECTED = 'disconnected';
    const EVENT_DELETED = 'deleted';

    public function __construct(UserService $userService)
    {
        $this->userService = $userService;
        
        $this->connection = new AMQPStreamConnection(
            env('RABBITMQ_HOST'),
            env('RABBITMQ_PORT'),
            env('RABBITMQ_USER'),
            env('RABBITMQ_PASSWORD')
        );

        $this->channel = $this->connection->channel();
        $this->initializeRabbitMQ();
    }

    private function initializeRabbitMQ(): void
    {
        // Exchange principal pour les événements utilisateur
        $this->channel->exchange_declare(
            'user_events', 
            'topic', // Type topic pour plus de flexibilité
            false, 
            true,  // durable
            false
        );

        // Queue pour les statuts (connexion/déconnexion)
        $this->channel->queue_declare(
            'user_status_updates',
            false,
            true,
            false,
            false
        );

        // Queue pour les suppressions
        $this->channel->queue_declare(
            'user_deletion_events',
            false,
            true,
            false,
            false
        );

        // Bindings
        $this->channel->queue_bind('user_status_updates', 'user_events', 'user.status.*');
        $this->channel->queue_bind('user_deletion_events', 'user_events', 'user.deleted');
    }

    public function listenForUserEvents()
    {
        // Callback pour les statuts
        $statusCallback = function ($msg) {
            try {
                $data = $this->validateMessage($msg, ['user_id', 'event']);
                
                match ($data['event']) {
                    self::EVENT_CONNECTED => $this->userService->handleUserConnection($data['user_id'], $data),
                    self::EVENT_DISCONNECTED => $this->userService->handleUserDisconnection($data['user_id']),
                    default => Log::warning("Événement de statut inconnu", ['event' => $data['event']])
                };

                $msg->ack();
            } catch (\Exception $e) {
                $this->handleError($msg, $e);
            }
        };

        // Callback pour les suppressions
        $deletionCallback = function ($msg) {
            try {
                $data = $this->validateMessage($msg, ['user_id']);
                $this->userService->deleteUser($data['user_id']);
                $msg->ack();
            } catch (\Exception $e) {
                $this->handleError($msg, $e);
            }
        };

        // Démarrage des consumers
        $this->channel->basic_consume(
            'user_status_updates',
            '',
            false,
            false,
            false,
            false,
            $statusCallback
        );

        $this->channel->basic_consume(
            'user_deletion_events',
            '',
            false,
            false,
            false,
            false,
            $deletionCallback
        );

        while ($this->channel->is_consuming()) {
            $this->channel->wait();
        }
    }

    private function validateMessage(AMQPMessage $msg, array $requiredFields): array
    {
        $data = json_decode($msg->getBody(), true, 512, JSON_THROW_ON_ERROR);
        
        foreach ($requiredFields as $field) {
            if (empty($data[$field])) {
                throw new \InvalidArgumentException("Champ manquant : $field");
            }
        }

        return $data;
    }

    private function handleError(AMQPMessage $msg, \Exception $e): void
    {
        Log::error("Erreur traitement message RabbitMQ", [
            'error' => $e->getMessage(),
            'body' => $msg->getBody(),
            'trace' => $e->getTraceAsString()
        ]);

        // NACK avec requeue sauf pour les erreurs de validation
        $msg->nack(!$e instanceof \InvalidArgumentException);
    }

    public function __destruct()
    {
        $this->channel->close();
        $this->connection->close();
    }
}