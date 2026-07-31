<?php

namespace App\Observers;

use App\Models\Property;
use Illuminate\Support\Facades\Log;

class PropertyObserver
{
    /**
     * Handle the Property "created" event.
     */
    public function created(Property $property): void
    {
        Log::info("Nueva propiedad creada (ID: {$property->id}). 
        Notificando a la IA...");
    }

    /**
     * Handle the Property "updated" event.
     */
    public function updated(Property $property): void
    {
        Log::info("Propiedad actualizada (ID: {$property->id}). ctualizando RAG...");
    }

    /**
     * Handle the Property "deleted" event.
     */
    public function deleted(Property $property): void
    {
        Log::info("Propiedad eliminada (ID: {$property->id}). Borrando del RAG...");
        
    }

    /**
     * Handle the Property "restored" event.
     */
    public function restored(Property $property): void
    {
        //
    }

    /**
     * Handle the Property "force deleted" event.
     */
    public function forceDeleted(Property $property): void
    {
        //
    }
}
