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
        Schema::create('properties', function (Blueprint $table) {
            $table->id();
            $table->string('title');
            $table->text('description');
            $table->string('zone');
            $table->decimal('price', 15, 2);
            $table->decimal('administration_fee', 15, 2)->default(0);
            $table->integer('area_m2');
            $table->integer('bedrooms');
            $table->integer('bathrooms');
            $table->json('amenities')->nullable();
            $table->enum('status', ['disponible', 'vendida', 'arrendada'])->default('disponible');
            $table->unsignedBigInteger('agent_id')->nullable();
            $table->timestamps();
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::dropIfExists('properties');
    }
};
