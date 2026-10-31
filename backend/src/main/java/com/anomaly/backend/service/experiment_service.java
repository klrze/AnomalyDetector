package com.anomaly.backend.service;

import com.anomaly.backend.entity.experiment_log;
import com.anomaly.backend.repository.experiment_repository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class experiment_service {

    private final experiment_repository experimentRepository;

    public List<experiment_log> getExperimentsByChannel(String channel) {
        return experimentRepository.findByChannel(channel);
    }
}