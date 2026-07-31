<?php

namespace Database\Factories;

use App\Models\Lead;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Lead>
 */
class LeadFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'name' => fake()->name(),
            'email' => fake()->safeEmail(),
            'phone' => fake()->phoneNumber(),
            'status' => fake()->randomElement(['nuevo', 'contactado', 'calificado', 'perdido']),
            'notes' => fake()->sentence(),
            // Busca un ID al azar de las propiedades y agentes que ya existen
            'property_id' => \App\Models\Property::inRandomOrder()->first()?->id,
            'agent_id' => \App\Models\Agent::inRandomOrder()->first()?->id,
        ];
    }
}
