<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Agent extends Model
{
    /** @use HasFactory<\Database\Factories\AgentFactory> */
    use HasFactory;

    protected $fillable = [
        'name', 'email', 'phone', 'zone', 'languages', 'working_hours', 'monthly_sales_count'
    ];

    protected $casts = [
        'languages' => 'array',
    ];
}
