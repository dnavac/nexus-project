<?php

namespace Database\Factories;

use App\Models\Property;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Property>
 */
class PropertyFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'title' => 'Inmueble en ' . fake()->streetName(),
            'description' => fake()->paragraph(),
            'zone' => fake()->randomElement(['Bocagrande', 'Castillogrande', 'Manga', 'Centro Histórico','El Laguito','Getsemani','Crespo','Cabrero','Canapote','Cielo Mar']),
            'price' => fake()->randomFloat(2, 300000000, 1500000000), // Precio entre 300M y 1.500M
            'administration_fee' => fake()->randomFloat(2, 200000, 1000000),
            'area_m2' => fake()->numberBetween(50, 400),
            'bedrooms' => fake()->numberBetween(1, 5),
            'bathrooms' => fake()->numberBetween(1, 4),
            'amenities' => fake()->randomElements(['Piscina', 'Gimnasio', 'Parqueadero', 'BBQ', 'Vigilancia'], 2),
            'status' => fake()->randomElement(['disponible', 'vendida', 'arrendada']),
            // Asigna un Agente al azar que ya exista en la BD
            'agent_id' => \App\Models\Agent::inRandomOrder()->first()->id ?? \App\Models\Agent::factory(),
        ];
    }
}
