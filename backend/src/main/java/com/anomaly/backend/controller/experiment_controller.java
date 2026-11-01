package com.anomaly.backend.controller;

import com.anomaly.backend.entity.experiment_log;
import com.anomaly.backend.service.experiment_service;
import lombok.RequiredArgsConstructor;

import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@CrossOrigin(origins = "http://localhost:5173")
@RestController
@RequestMapping("/api/experiments")
@RequiredArgsConstructor
public class experiment_controller {

    private final experiment_service experimentService;

    @GetMapping("/channel/{channel}")
    public ResponseEntity<List<experiment_log>> getExperimentsByChannel(@PathVariable String channel) {
        List<experiment_log> experiments = experimentService.getExperimentsByChannel(channel);
        return ResponseEntity.ok(experiments);
    }

    @GetMapping("/channel/{channel}/best")
    public ResponseEntity<experiment_log> getBestExperiment(@PathVariable String channel) {
        experiment_log best = experimentService.getBestExperimentByChannel(channel);
        return ResponseEntity.ok(best);
    }
}