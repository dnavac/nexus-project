<?php

namespace Database\Factories;

use App\Models\Transaction;
use Illuminate\Database\Eloquent\Factories\Factory;

/**
 * @extends Factory<Transaction>
 */
class TransactionFactory extends Factory
{
    /**
     * Define the model's default state.
     *
     * @return array<string, mixed>
     */
    public function definition(): array
    {
        return [
            'property_id' => \App\Models\Property::inRandomOrder()->first()?->id ?? 1,
            'agent_id' => \App\Models\Agent::inRandomOrder()->first()?->id ?? 1,
            'lead_id' => \App\Models\Lead::inRandomOrder()->first()?->id ?? 1,
            'amount' => fake()->randomFloat(2, 2000000, 1500000000),
            'transaction_date' => fake()->dateTimeBetween('-1 year', 'now'),
            'type' => fake()->randomElement(['venta', 'arriendo']),
        ];
    }
}
