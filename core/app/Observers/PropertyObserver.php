<?php

namespace App\Observers;

use App\Models\Property;
use App\Jobs\SyncRagDocument;
use Illuminate\Support\Facades\Log;

class PropertyObserver
{
    /**
     * Handle the Property "created" event.
     */
    public function created(Property $property): void
    {
        SyncRagDocument::dispatchSync('properties', 'created', $property->toArray());
    }

    /**
     * Handle the Property "updated" event.
     */
    public function updated(Property $property): void
    {
        SyncRagDocument::dispatchSync('properties', 'updated', $property->toArray());
    }

    /**
     * Handle the Property "deleted" event.
     */
    public function deleted(Property $property): void
    {
        SyncRagDocument::dispatchSync('properties', 'deleted', ['id' => $property->id]);
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
