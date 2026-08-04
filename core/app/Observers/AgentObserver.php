<?php

namespace App\Observers;

use App\Jobs\SyncRagDocument;
use App\Models\Agent;

class AgentObserver
{
    public function created(Agent $model): void { SyncRagDocument::dispatchSync('agents', 'created', $model->toArray()); }
    public function updated(Agent $model): void { SyncRagDocument::dispatchSync('agents', 'updated', $model->toArray()); }
    public function deleted(Agent $model): void { SyncRagDocument::dispatchSync('agents', 'deleted', ['id' => $model->id]); }
}
