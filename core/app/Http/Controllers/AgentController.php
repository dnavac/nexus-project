<?php

namespace App\Http\Controllers;

use App\Models\Agent;
use App\Http\Requests\StoreAgentRequest;
use App\Http\Requests\UpdateAgentRequest;

class AgentController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $agents = Agent::all();
        return response()->json([
            'message' => 'Agentes obtenidos correctamente',
            'agents' => $agents
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
    public function store(StoreAgentRequest $request)
    {
        $agent = Agent::create($request->all());
        return response()->json([
            'message' => 'Agente creado correctamente',
            'agent' => $agent
        ], 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Agent $agent)
    {
        return response()->json([
            'message' => 'Agente obtenido correctamente',
            'agent' => $agent
        ], 200);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Agent $agent)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(UpdateAgentRequest $request, Agent $agent)
    {
        $agent->update($request->all());
        return response()->json([
            'message' => 'Agente actualizado correctamente',
            'agent' => $agent
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Agent $agent)
    {
        $agent->delete();
        return response()->json([
            'message' => 'Agente eliminado correctamente'
        ], 200);
    }
}
