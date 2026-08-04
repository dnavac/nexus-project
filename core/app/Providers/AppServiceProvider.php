<?php

namespace App\Providers;

use Illuminate\Support\ServiceProvider;
use App\Models\Property;
use App\Observers\PropertyObserver;
use App\Models\Agent;
use App\Models\Lead;
use App\Models\Transaction;
use App\Observers\AgentObserver;
use App\Observers\LeadObserver;
use App\Observers\TransactionObserver;

class AppServiceProvider extends ServiceProvider
{
    /**
     * Register any application services.
     */
    public function register(): void
    {
        //
    }

    /**
     * Bootstrap any application services.
     */
    public function boot(): void
    {
        Property::observe(PropertyObserver::class);
        Agent::observe(AgentObserver::class);
        Lead::observe(LeadObserver::class);
        Transaction::observe(TransactionObserver::class);
    }
}
