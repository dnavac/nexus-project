<?php

namespace App\Observers;

use App\Jobs\SyncRagDocument;
use App\Models\Lead;

class LeadObserver
{
    public function created(Lead $model): void { SyncRagDocument::dispatchSync('leads', 'created', $model->toArray()); }
    public function updated(Lead $model): void { SyncRagDocument::dispatchSync('leads', 'updated', $model->toArray()); }
    public function deleted(Lead $model): void { SyncRagDocument::dispatchSync('leads', 'deleted', ['id' => $model->id]); }
}
