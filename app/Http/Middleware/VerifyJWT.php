<?php

namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;
use Symfony\Component\HttpFoundation\Response;
use App\Services\JwtService;
use App\Services\UserService;

class VerifyJWT{

    private $jwtService;
    private $userService;

    public function __construct(JwtService $jwtService, UserService $userService)
    {
        $this->jwtService = $jwtService;
        $this->userService = $userService;
    }
    /**
     * Handle an incoming request.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {   

        // Vérifier si JWT est désactivé
        if (env('JWT_ENABLED', true) === false) {
            return $next($request);
        }

        $token = $request->bearerToken();

        if (!$token) {
            return response()->json(['error' => 'Token missing'], 401);
        }

        $decoded = $this->jwtService->validateToken($token);

        if (!$decoded) {
            return response()->json(['error' => 'Invalid token'], 401);
        }

        $userId = $decoded['user_id'];
        $user = $this->userService->getUser($userId);

        if (!$user || !$this->userService->isUserActive($userId)) {
            return response()->json(['error' => 'Unauthorized'], 401);
        }

        return $next($request);
    }
}
