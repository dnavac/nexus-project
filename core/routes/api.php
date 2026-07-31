<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Http\Controllers\AgentController;
use App\Http\Controllers\LeadController;
use App\Http\Controllers\PropertyController;
use App\Http\Controllers\TransactionController;

//Rutas CRUD de los 4 modelos principales.
Route::apiResource('agents', AgentController::class);
Route::apiResource('leads', LeadController::class);
Route::apiResource('properties', PropertyController::class);
Route::apiResource('transactions', TransactionController::class);
