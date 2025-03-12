Si vous utilisez la bibliothèque **firebase/php-jwt** pour gérer les tokens JWT dans votre projet Laravel, vous devrez implémenter manuellement la logique de vérification du token dans un middleware personnalisé. Contrairement à `tymon/jwt-auth`, `firebase/php-jwt` ne fournit pas de middleware prêt à l'emploi, mais elle offre une API simple pour encoder et décoder les tokens JWT.

Voici comment vous pouvez implémenter un middleware personnalisé pour vérifier la validité d'un token JWT en utilisant `firebase/php-jwt`.

---

### Étape 1 : Installer la dépendance `firebase/php-jwt`
Installez la bibliothèque via Composer :
```bash
composer require firebase/php-jwt
```

---

### Étape 2 : Créer un Middleware Personnalisé
Générez un middleware personnalisé pour vérifier les tokens JWT.

1. Créez le middleware :
   ```bash
   php artisan make:middleware VerifyJWT
   ```

2. Implémentez la logique de vérification du token dans le middleware (`app/Http/Middleware/VerifyJWT.php`) :
   ```php
   namespace App\Http\Middleware;

   use Closure;
   use Firebase\JWT\JWT;
   use Firebase\JWT\Key;
   use Firebase\JWT\ExpiredException;
   use Firebase\JWT\SignatureInvalidException;
   use Exception;
   use Illuminate\Http\Request;

   class VerifyJWT
   {
       public function handle(Request $request, Closure $next)
       {
           // Récupérer le token depuis l'en-tête Authorization
           $token = $request->header('Authorization');

           if (!$token) {
               return response()->json(['message' => 'Token manquant'], 401);
           }

           // Supprimer le préfixe "Bearer " du token
           $token = str_replace('Bearer ', '', $token);

           try {
               // Clé secrète utilisée pour signer le token
               $secretKey = env('JWT_SECRET');

               // Décoder et vérifier le token
               $decoded = JWT::decode($token, new Key($secretKey, 'HS256'));

               // Ajouter les informations du token à la requête
               $request->auth = $decoded;

           } catch (ExpiredException $e) {
               return response()->json(['message' => 'Token expiré'], 401);
           } catch (SignatureInvalidException $e) {
               return response()->json(['message' => 'Token invalide'], 401);
           } catch (Exception $e) {
               return response()->json(['message' => 'Erreur de vérification du token'], 401);
           }

           // Passer à la prochaine étape
           return $next($request);
       }
   }
   ```

---

### Étape 3 : Enregistrer le Middleware
Enregistrez votre middleware personnalisé dans `app/Http/Kernel.php` :
```php
protected $routeMiddleware = [
    // ...
    'jwt.verify' => \App\Http\Middleware\VerifyJWT::class,
];
```

---

### Étape 4 : Utiliser le Middleware dans les Routes
Appliquez le middleware `jwt.verify` aux routes que vous souhaitez protéger.

**Exemple dans `routes/api.php` :**
```php
use Illuminate\Support\Facades\Route;

Route::middleware('jwt.verify')->group(function () {
    // Routes protégées par JWT
    Route::get('/profile', 'ProfileController@show');
});
```

---

### Étape 5 : Générer un Token JWT
Pour générer un token JWT lors de la connexion de l'utilisateur, utilisez la bibliothèque `firebase/php-jwt`.

**Exemple dans un contrôleur :**
```php
use Firebase\JWT\JWT;
use Firebase\JWT\Key;

class AuthController extends Controller
{
    public function login(Request $request)
    {
        // Valider les identifiants de l'utilisateur
        $credentials = $request->only('email', 'password');

        if (!auth()->attempt($credentials)) {
            return response()->json(['message' => 'Identifiants invalides'], 401);
        }

        // Créer le payload du token
        $payload = [
            'iss' => "your-app-name", // Émetteur du token
            'sub' => auth()->user()->id, // Sujet du token (ID de l'utilisateur)
            'iat' => time(), // Heure d'émission
            'exp' => time() + 3600 // Heure d'expiration (1 heure)
        ];

        // Générer le token
        $secretKey = env('JWT_SECRET');
        $token = JWT::encode($payload, $secretKey, 'HS256');

        return response()->json(['token' => $token]);
    }
}
```

---

### Étape 6 : Tester le Middleware
1. **Connexion** :
   - Envoyez une requête POST à `/login` avec les identifiants de l'utilisateur.
   - Le serveur renvoie un token JWT.

2. **Accès à une ressource protégée** :
   - Envoyez une requête GET à `/profile` avec le token JWT dans l'en-tête `Authorization`.
   - Si le token est valide, la requête est traitée.
   - Si le token est invalide ou expiré, une erreur `401 Unauthorized` est renvoyée.

---

### Exemple de Réponse en Cas d'Erreur
Si le token est invalide ou expiré, la réponse JSON ressemblera à ceci :
```json
{
    "message": "Token expiré",
    "status": 401
}
```

---

### Conclusion
En utilisant `firebase/php-jwt`, vous avez un contrôle total sur la gestion des tokens JWT dans votre application Laravel. Bien que cela nécessite un peu plus de travail manuel que `tymon/jwt-auth`, cela vous permet de personnaliser entièrement le processus d'authentification et de validation des tokens. Le middleware personnalisé que vous avez créé peut être adapté pour répondre à des besoins spécifiques, comme l'ajout de claims personnalisés ou la gestion de tokens rafraîchis.







Pour désactiver temporairement la sécurité JWT dans votre application Laravel afin de faciliter les tests, vous avez plusieurs options. Voici les méthodes les plus courantes, en fonction de vos besoins :

---

### 1. **Commenter ou Supprimer le Middleware JWT dans les Routes**
Si vous avez appliqué le middleware JWT au niveau des routes, vous pouvez simplement commenter ou supprimer temporairement le middleware pour désactiver la vérification du token.

**Exemple :**
```php
// Avant (avec sécurité JWT)
Route::middleware('jwt.verify')->group(function () {
    Route::get('/profile', 'ProfileController@show');
});

// Après (sans sécurité JWT)
Route::get('/profile', 'ProfileController@show');
```

Cette méthode est rapide et facile, mais elle nécessite de modifier manuellement les routes.

---

### 2. **Utiliser une Variable d'Environnement pour Activer/Désactiver JWT**
Vous pouvez ajouter une variable d'environnement dans votre fichier `.env` pour activer ou désactiver la sécurité JWT. Ensuite, utilisez cette variable dans votre middleware pour ignorer la vérification du token.

#### Étape 1 : Ajouter une Variable dans `.env`
Ajoutez une variable comme `JWT_ENABLED` dans votre fichier `.env` :
```env
JWT_ENABLED=true
```

#### Étape 2 : Modifier le Middleware
Modifiez votre middleware pour vérifier la valeur de cette variable avant de valider le token.

**Exemple dans `app/Http/Middleware/VerifyJWT.php` :**
```php
public function handle(Request $request, Closure $next)
{
    // Vérifier si JWT est désactivé
    if (env('JWT_ENABLED', true) === false) {
        return $next($request);
    }

    // Logique de vérification du token JWT
    $token = $request->header('Authorization');

    if (!$token) {
        return response()->json(['message' => 'Token manquant'], 401);
    }

    $token = str_replace('Bearer ', '', $token);

    try {
        $secretKey = env('JWT_SECRET');
        $decoded = JWT::decode($token, new Key($secretKey, 'HS256'));
        $request->auth = $decoded;
    } catch (ExpiredException $e) {
        return response()->json(['message' => 'Token expiré'], 401);
    } catch (SignatureInvalidException $e) {
        return response()->json(['message' => 'Token invalide'], 401);
    } catch (Exception $e) {
        return response()->json(['message' => 'Erreur de vérification du token'], 401);
    }

    return $next($request);
}
```

#### Étape 3 : Désactiver JWT dans `.env`
Pour désactiver JWT, modifiez la variable dans `.env` :
```env
JWT_ENABLED=false
```

Cette méthode est plus flexible et vous permet de basculer facilement entre les modes de test et de production.

---

### 3. **Utiliser un Utilisateur Factice pour les Tests**
Si vous souhaitez tester l'application sans désactiver complètement JWT, vous pouvez simuler un utilisateur authentifié en utilisant un utilisateur factice dans vos tests.

#### Étape 1 : Créer un Utilisateur Factice
Dans votre middleware, ajoutez une condition pour simuler un utilisateur authentifié lorsque vous êtes en mode test.

**Exemple dans `app/Http/Middleware/VerifyJWT.php` :**
```php
public function handle(Request $request, Closure $next)
{
    // Mode test : simuler un utilisateur authentifié
    if (env('APP_ENV') === 'testing') {
        $user = User::first(); // Récupérer un utilisateur factice
        auth()->login($user); // Authentifier l'utilisateur
        return $next($request);
    }

    // Logique de vérification du token JWT
    $token = $request->header('Authorization');

    if (!$token) {
        return response()->json(['message' => 'Token manquant'], 401);
    }

    $token = str_replace('Bearer ', '', $token);

    try {
        $secretKey = env('JWT_SECRET');
        $decoded = JWT::decode($token, new Key($secretKey, 'HS256'));
        $request->auth = $decoded;
    } catch (ExpiredException $e) {
        return response()->json(['message' => 'Token expiré'], 401);
    } catch (SignatureInvalidException $e) {
        return response()->json(['message' => 'Token invalide'], 401);
    } catch (Exception $e) {
        return response()->json(['message' => 'Erreur de vérification du token'], 401);
    }

    return $next($request);
}
```

#### Étape 2 : Configurer l'Environnement de Test
Assurez-vous que votre environnement de test est configuré correctement dans `.env.testing` :
```env
APP_ENV=testing
```

---

### 4. **Utiliser un Middleware de Test**
Vous pouvez créer un middleware de test qui remplace temporairement le middleware JWT. Ce middleware ignorera la vérification du token et permettra l'accès à toutes les routes.

#### Étape 1 : Créer un Middleware de Test
Générez un middleware de test :
```bash
php artisan make:middleware DisableJWT
```

#### Étape 2 : Implémenter le Middleware de Test
Dans `app/Http/Middleware/DisableJWT.php`, ajoutez simplement la logique pour passer à la prochaine étape :
```php
namespace App\Http\Middleware;

use Closure;
use Illuminate\Http\Request;

class DisableJWT
{
    public function handle(Request $request, Closure $next)
    {
        // Ignorer la vérification du token
        return $next($request);
    }
}
```

#### Étape 3 : Remplacer le Middleware JWT par le Middleware de Test
Dans `app/Http/Kernel.php`, remplacez temporairement le middleware JWT par le middleware de test :
```php
protected $routeMiddleware = [
    // 'jwt.verify' => \App\Http\Middleware\VerifyJWT::class, // Commenter ou supprimer
    'jwt.verify' => \App\Http\Middleware\DisableJWT::class, // Utiliser le middleware de test
];
```

---

### Conclusion
Pour désactiver temporairement la sécurité JWT dans votre application Laravel, vous pouvez :
1. Commenter ou supprimer le middleware JWT dans les routes.
2. Utiliser une variable d'environnement pour activer/désactiver JWT.
3. Simuler un utilisateur authentifié en mode test.
4. Remplacer le middleware JWT par un middleware de test.

Chaque méthode a ses avantages, alors choisissez celle qui correspond le mieux à vos besoins de test. N'oubliez pas de réactiver la sécurité JWT une fois les tests terminés pour garantir la sécurité de votre application en production.