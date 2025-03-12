<?php

namespace App\Services;

use Firebase\JWT\JWT;
use Firebase\JWT\Key;
use Illuminate\Support\Facades\Log;

class JwtService
{
    private $key;

    public function __construct()
    {
        $this->key = config('app.jwt.secret'); // Clé secrète JWT
    }

    /**
     * Valider un token JWT.
     */
    public function validateToken($token)
    {
        try {
            $decoded = JWT::decode($token, new Key($this->key, 'HS256'));
            return (array) $decoded;
        } catch (\Exception $e) {
            Log::error('Erreur lors de la validation du Token : ' . $e->getMessage());
            // throw $e; 
            return null;
        }
    }
}