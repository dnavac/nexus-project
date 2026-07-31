<?php

namespace App\Http\Controllers;

use App\Models\Transaction;
use App\Http\Requests\StoreTransactionRequest;
use App\Http\Requests\UpdateTransactionRequest;

class TransactionController extends Controller
{
    /**
     * Display a listing of the resource.
     */
    public function index()
    {
        $transactions = Transaction::all();
        return response()->json([
            'message' => 'Transacciones obtenidas correctamente',
            'transactions' => $transactions
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
    public function store(StoreTransactionRequest $request)
    {
        $transaction = Transaction::create($request->all());
        return response()->json([
            'message' => 'Transaccion creada correctamente',
            'transaction' => $transaction
        ], 201);
    }

    /**
     * Display the specified resource.
     */
    public function show(Transaction $transaction)
    {
        return response()->json([
            'message' => 'Transaccion obtenida correctamente',
            'transaction' => $transaction
        ], 200);
    }

    /**
     * Show the form for editing the specified resource.
     */
    public function edit(Transaction $transaction)
    {
        //
    }

    /**
     * Update the specified resource in storage.
     */
    public function update(UpdateTransactionRequest $request, Transaction $transaction)
    {
        $transaction->update($request->all());
        return response()->json([
            'message' => 'Transaccion actualizada correctamente',
            'transaction' => $transaction
        ], 200);
    }

    /**
     * Remove the specified resource from storage.
     */
    public function destroy(Transaction $transaction)
    {
        $transaction->delete();
        return response()->json([
            'message' => 'Transaccion eliminada correctamente'
        ], 200);
    }
}
