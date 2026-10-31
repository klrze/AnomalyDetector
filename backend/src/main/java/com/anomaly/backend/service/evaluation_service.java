package com.anomaly.backend.service;

import com.anomaly.backend.entity.evaluation_log;
import com.anomaly.backend.repository.evaluation_repository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
@RequiredArgsConstructor
public class evaluation_service {

    private final evaluation_repository evaluationRepository;

    public List<evaluation_log> getEvaluationsByChannel(String channel) {
        return evaluationRepository.findByChannel(channel);
    }
}