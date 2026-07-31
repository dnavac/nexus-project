<?php

namespace App\Http\Controllers;

use App\Models\Lead;
use App\Http\Requests\StoreLeadRequest;
use App\Http\Requests\UpdateLeadRequest;

class LeadController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $leads = Lead::all();
        return response()->json([
            'message' => 'Leads obtenidos correctamente',
            'leads' => $leads
        ], 200);
    }

    /**
     * Show the form for creating a new resource.
     */
    public function create()
    {
        //
    }

    /**
     * Store a newly created resource in storage.
     */
    public function store(StoreLeadRequest $request)
    {
        $lead = Lead::create($request->all());
        return response()->json([
            'message' => 'Lead creado correctamente',
            'lead' => $lead
        ], 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Lead $lead)
    {
        return response()->json([
            'message' => 'Lead obtenido correctamente',
            'lead' => $lead
        ], 200);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Lead $lead)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(UpdateLeadRequest $request, Lead $lead)
    {
        $lead->update($request->all());
        return response()->json([
            'message' => 'Lead actualizado correctamente',
            'lead' => $lead
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Lead $lead)
    {
        $lead->delete();
        return response()->json([
            'message' => 'Lead eliminado correctamente'
        ], 200);
    }
}
