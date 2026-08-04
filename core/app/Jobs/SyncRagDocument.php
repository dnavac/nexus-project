<?php

namespace App\Jobs;

use Illuminate\Bus\Queueable;
use Illuminate\Contracts\Queue\ShouldQueue;
use Illuminate\Foundation\Bus\Dispatchable;
use Illuminate\Queue\InteractsWithQueue;
use Illuminate\Queue\SerializesModels;
use Illuminate\Support\Facades\Http;
use Illuminate\Support\Facades\Log;

class SyncRagDocument implements ShouldQueue
{
    use Dispatchable, InteractsWithQueue, Queueable, SerializesModels;

    public function __construct(
        public string $table,
        public string $event,
        public array $row,
    ) {}

    public function handle(): void
    {
        $response = Http::timeout(10)->post(
            rtrim(config('services.nexus_ai.rag_url'), '/') . '/sync',
            ['table' => $this->table, 'event' => $this->event, 'row' => $this->row]
        );

        if ($response->failed()) {
            Log::warning('RAG sync failed', [
                'table' => $this->table,
                'id' => $this->row['id'] ?? null,
                'status' => $response->status(),
                'body' => $response->body(),
            ]);
        }
    }
}
