<?php

namespace App\Observers;

use App\Jobs\SyncRagDocument;
use App\Models\Transaction;

class TransactionObserver
{
    public function created(Transaction $model): void { SyncRagDocument::dispatchSync('transactions', 'created', $model->toArray()); }
    public function updated(Transaction $model): void { SyncRagDocument::dispatchSync('transactions', 'updated', $model->toArray()); }
    public function deleted(Transaction $model): void { SyncRagDocument::dispatchSync('transactions', 'deleted', ['id' => $model->id]); }
}
