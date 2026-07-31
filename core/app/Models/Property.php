<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;

class Property extends Model
{
    /** @use HasFactory<\Database\Factories\PropertyFactory> */
    use HasFactory;

    protected $fillable = [
        'title', 'description', 'zone', 'price', 'administration_fee',
        'area_m2', 'bedrooms', 'bathrooms', 'amenities', 'status', 'agent_id'
    ];

    protected $casts = [
        'amenities' => 'array',
    ];
}
