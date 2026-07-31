<?php

namespace App\Http\Controllers;

use App\Models\Property;
use App\Http\Requests\StorePropertyRequest;
use App\Http\Requests\UpdatePropertyRequest;

class PropertyController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $property = Property::all();
        return response()->json([
            'message' => 'Propiedades obtenidas correctamente',
            'properties' => $property
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
    public function store(StorePropertyRequest $request)
    {
        $property = Property::create($request->all());
        return response()->json([
            'message' => 'Propiedad creada correctamente',
            'property' => $property
        ], 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Property $property)
    {
        return response()->json([
            'message' => 'Propiedad obtenida correctamente',
            'property' => $property
        ], 200);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Property $property)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(UpdatePropertyRequest $request, Property $property)
    {
        $property->update($request->all());
        return response()->json([
            'message' => 'Propiedad actualizada correctamente',
            'property' => $property
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Property $property)
    {
        $property->delete();
        return response()->json([
            'message' => 'Propiedad eliminada correctamente'
        ], 200);
    }
}
