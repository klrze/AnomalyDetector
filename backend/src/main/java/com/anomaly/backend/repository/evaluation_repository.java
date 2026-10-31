package com.anomaly.backend.repository;

import com.anomaly.backend.entity.evaluation_log;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

import java.util.List;

@Repository
public interface evaluation_repository extends JpaRepository<evaluation_log, Long> {
    
    List<evaluation_log> findByChannel(String channel);
}