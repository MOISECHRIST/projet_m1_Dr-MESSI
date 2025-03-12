<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {



        Schema::create('publications', function (Blueprint $table) {
            $table->id(); 
            $table->unsignedBigInteger('author_id');
            $table->string('title'); 
            $table->text('description');
            $table->timestamps();
            $table->enum('type', ['Video', 'TextImage']);
            $table->json('image_urls')->nullable(); 
            $table->string('video_url')->nullable(); 
            $table->string('textContent')->nullable(); 
            $table->Integer('nbr_view')->nullable();
            $table->foreignId('user_id')->constrained()->onDelete('cascade');
            
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {   
        Schema::dropIfExists('publications');
    }
};
